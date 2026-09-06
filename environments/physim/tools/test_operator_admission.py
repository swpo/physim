"""Operator-only startup fence tests. No inference or physics runs."""
import json,os,pathlib,subprocess,sys,tempfile,unittest
from physim.operator_admission import check_new_server_admission,write_fence,process_identity,OperatorAdmissionClosed

class AdmissionTests(unittest.TestCase):
    def test_exact_match_only(self):
        with tempfile.TemporaryDirectory() as d:
            identity={"pid":321,"birth":"Sat Sep 5 17:32:25 2026","command_sha256":"a"*64}
            write_fence(identity,directory=d)
            with self.assertRaises(OperatorAdmissionClosed):
                check_new_server_admission(parent_pid=321,directory=d,identity_reader=lambda p:identity)
            check_new_server_admission(parent_pid=999,directory=d,identity_reader=lambda p:identity)
            check_new_server_admission(parent_pid=321,directory=d,identity_reader=lambda p:{**identity,"birth":"different"})
            check_new_server_admission(parent_pid=321,directory=d,identity_reader=lambda p:{**identity,"command_sha256":"b"*64})
            events=[json.loads(x) for x in (pathlib.Path(d)/"events.jsonl").read_text().splitlines()]
            self.assertEqual(len(events),1)
            self.assertEqual(events[0]["classification"],"not_admitted_by_operator")
    def test_real_module_boot_stops_before_server(self):
        with tempfile.TemporaryDirectory() as d:
            identity=process_identity(os.getpid()); self.assertIsNotNone(identity)
            write_fence(identity,directory=d)
            port=pathlib.Path(d)/"port"
            env={**os.environ,"PHYSIM_OPERATOR_ADMISSION_DIR":d,"MCP_PORT_FILE":str(port),"VF_CONFIG":'{"r5_mode":true,"r5_resource_policy":"v2r2"}'}
            proc=subprocess.run([sys.executable,"-m","physim.servers.blob"],env=env,capture_output=True,text=True,timeout=20)
            self.assertEqual(proc.returncode,78,proc.stdout+proc.stderr)
            self.assertIn("PHYSIM_OPERATOR_ADMISSION_CLOSED",proc.stderr)
            self.assertFalse(port.exists())
    def test_import_does_not_gate_active_objects(self):
        with tempfile.TemporaryDirectory() as d:
            write_fence(process_identity(os.getpid()),directory=d)
            env={**os.environ,"PHYSIM_OPERATOR_ADMISSION_DIR":d}
            proc=subprocess.run([sys.executable,"-c","import physim.servers.blob; print('IMPORT_OK')"],env=env,capture_output=True,text=True,timeout=20)
            self.assertEqual(proc.returncode,0,proc.stderr)
            self.assertIn("IMPORT_OK",proc.stdout)
            self.assertFalse((pathlib.Path(d)/"events.jsonl").exists())

if __name__=='__main__': unittest.main()
