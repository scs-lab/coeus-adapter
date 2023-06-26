from py_coeus_ci.test_manager import TestManager
from jarvis_util import *

class NativeTestManager(TestManager):
    def spawn_all_nodes(self):
        return self.spawn_info()

    def set_paths(self):
        self.BASIC_CMD = f"{self.CMAKE_BINARY_DIR}/bin/basic"
        self.GraySIM_CMD = f"{self.CMAKE_BINARY_DIR}/bin/adios2-gray-scott"
        self.GrayCalc_CMD = f"{self.CMAKE_BINARY_DIR}/bin/adios2-pdf-calc"
        self.Simulation_Path = f"{self.CMAKE_SOURCE_DIR}/test/real_apps/gray-scott/simulation"
        self.gsbp_path = f"{self.CMAKE_BINARY_DIR}/test/real_apps/gray-scott"

    def test_basic(self):
            spawn_info = self.spawn_info(nprocs=1,
                                         hermes_conf='hermes_server')
            self.start_daemon(spawn_info)
            node = Exec(self.BASIC_CMD, spawn_info)
            self.stop_daemon(spawn_info)
            return node.exit_code

    def test_gray_scott_simulation_file(self):
        spawn_info = self.spawn_info(nprocs=1,
                                     hermes_conf='hermes_server')
        self.start_daemon(spawn_info)
        simulation = Exec(f"mpirun {self.GraySIM_CMD} {self.Simulation_Path}/settings-files.json", spawn_info)
        self.stop_daemon(spawn_info)
        return simulation.exit_code

    def test_gray_scott_analysis_file(self):
        spawn_info = self.spawn_info(nprocs=1,
                                     hermes_conf='hermes_server')
        self.start_daemon(spawn_info)
        simulation = Exec(f"mpirun {self.GraySIM_CMD} {self.Simulation_Path}/settings-files.json", spawn_info)
        analysis = Exec(f"mpirun {self.GrayCalc_CMD} {self.gsbp_path}/gs.bp {self.gsbp_path}/pdf.bp 100", spawn_info)
        self.stop_daemon(spawn_info)
        return simulation.exit_code + analysis.exit_code

    def test_gray_scott_simulation_file_parallel(self):
        spawn_info = self.spawn_info(nprocs=1,
                                     hermes_conf='hermes_server')
        self.start_daemon(spawn_info)
        simulation = Exec(f"mpirun -n 4 {self.GraySIM_CMD} {self.Simulation_Path}/settings-files.json", spawn_info)
        self.stop_daemon(spawn_info)
        return simulation.exit_code

    def test_gray_scott_analysis_file_parallel(self):
        spawn_info = self.spawn_info(nprocs=1,
                                     hermes_conf='hermes_server')
        self.start_daemon(spawn_info)
        simulation = Exec(f"mpirun -n 4 {self.GraySIM_CMD} {self.Simulation_Path}/settings-files.json", spawn_info)
        analysis = Exec(f"mpirun -n 2 {self.GrayCalc_CMD} {self.gsbp_path}/gs.bp {self.gsbp_path}/pdf.bp 100", spawn_info)
        self.stop_daemon(spawn_info)
        return simulation.exit_code + analysis.exit_code
