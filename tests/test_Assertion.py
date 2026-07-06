from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks

from knit_script.knit_script_interpreter.knitscript_logging.knitscript_logger import KnitScript_Error_Log


class TestAssertion(TestCase):
    def test_failed_assertion(self):
        program = r"""assert 1==2, "failure"; """
        with self.assertRaises(AssertionError):
            interpret_test_ks(program, print_k_lines=False, error_logger=KnitScript_Error_Log(log_to_console=False))

        program = r"""assert 1==2; """
        with self.assertRaises(AssertionError):
            interpret_test_ks(program, print_k_lines=False, error_logger=KnitScript_Error_Log(log_to_console=False))
