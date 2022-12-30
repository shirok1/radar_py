{ lib
, stdenv
, requireFile
, autoPatchelfHook
, autoAddOpenGLRunpathHook
, cudaVersion
, cudatoolkit
, cudnn
}:

{ pkgVer
, pkgDate
, sha256
}:

stdenv.mkDerivation rec {
  pname = "hikvision-mvs-${pkgVer}";
  version = fullVersion;
  src = fetchUrl {
    url = "https://www.hikrobotics.com/cn2/source/support/software/MVS_STD_GML_V${pkgVer}_${pkgDate}.zip";
    sha256 = sha256;
  };

  outputs = [ "out" "dev" ];

  nativeBuildInputs = [
    autoPatchelfHook
    autoAddOpenGLRunpathHook
  ];

  # Used by autoPatchelfHook
  buildInputs = [
  ];

  sourceRoot = "TensorRT-${version}";

  installPhase = ''
    install --directory "$dev" "$out"
    mv include "$dev"
    mv targets/x86_64-linux-gnu/lib "$out"
    install -D --target-directory="$out/bin" targets/x86_64-linux-gnu/bin/trtexec
  '';

  # Tell autoPatchelf about runtime dependencies.
  # (postFixup phase is run before autoPatchelfHook.)
  postFixup =
    let
      mostOfVersion = builtins.concatStringsSep "."
        (lib.take 3 (lib.versions.splitVersion version));
    in
    ''
      echo 'Patching RPATH of libnvinfer libs'
      patchelf --debug --add-needed libnvinfer.so \
        "$out/lib/libnvinfer.so.${mostOfVersion}" \
        "$out/lib/libnvinfer_plugin.so.${mostOfVersion}" \
        "$out/lib/libnvinfer_builder_resource.so.${mostOfVersion}"
    '';

  # meta = with lib; {
  #   # Check that the cudatoolkit version satisfies our min/max constraints (both
  #   # inclusive). We mark the package as broken if it fails to satisfies the
  #   # official version constraints (as recorded in default.nix). In some cases
  #   # you _may_ be able to smudge version constraints, just know that you're
  #   # embarking into unknown and unsupported territory when doing so.
  #   broken = !(elem cudaVersion supportedCudaVersions);
  #   description = "TensorRT: a high-performance deep learning interface";
  #   homepage = "https://developer.nvidia.com/tensorrt";
  #   license = licenses.unfree;
  #   platforms = [ "x86_64-linux" ];
  #   maintainers = with maintainers; [ aidalgol ];
  # };
}
