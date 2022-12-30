{ sources ? import ./nix/sources.nix
, pkgs ? import sources.nixpkgs {}
, nixgl ? import sources.nixgl {}
}:
let
  python310Optimized = pkgs.python310.override {
    enableOptimizations = true;
    reproducibleBuild = false;
    self = python310Optimized;
  };
  pythonEnv = python310Optimized.withPackages (ps: with ps; [
    pycuda
    pyqt5
    numpy
    tensorrt
    opencv4
    pyserial

    protobuf
    
    ipython
  ]);
in pkgs.mkShell {
  buildInputs = with pkgs; [
    pythonEnv
    cudaPackages.cudatoolkit
    cudaPackages.tensorrt
    nvtop-nvidia
    libsForQt5.qt5.qtx11extras
    libsForQt5.qt5.qtbase
    libsForQt5.qt5.qtwayland
    nixgl.auto.nixGLNvidia
    protobuf
  ];
  shellHook = ''
   '';
}
