from unittest import TestCase

from knitout_interpreter.knitout_errors.Knitout_Error import Knitout_Machine_StateError
from knitout_interpreter.knitout_execution_structures.Knitout_Knitting_Machine import Knitout_Machine_Specification
from resources.interpret_test_ks import interpret_test_ks
from resources.load_test_resources import load_test_resource

from knit_script.knit_script_errors.Knit_Script_Error import Incompatible_In_Carriage_Pass_Error


class TestKnit_Script_Exception(TestCase):

    def test_incompatible_carriage_pass_error(self):
        program = r"""
        Carrier = 1;
        in Leftward direction:{
            tuck f2;
            tuck f1;
        }
        in Rightward direction:{
            knit f1;
            miss f2;
        }
        """
        with self.assertRaises(Incompatible_In_Carriage_Pass_Error):
            interpret_test_ks(program, print_k_lines=False)

    def test_max_rack_error(self):
        program = load_test_resource("rack_6.ks")
        with self.assertRaises(Knitout_Machine_StateError):
            interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False)
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False, knitout_machine_spec=Knitout_Machine_Specification(maximum_rack=6), execute_knitout=False)
