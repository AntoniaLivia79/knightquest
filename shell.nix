with import <nixpkgs> {};
with pkgs.python3Packages;

buildPythonPackage rec {
  name = "knightquest";
  src = ./src;
  propagatedBuildInputs = [ python3Packages.numpy python3Packages.pygame python3Packages.maison ];
}
