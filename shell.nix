with import <nixpkgs> {};
with pkgs.python3Packages;

buildPythonPackage rec {
  name = "knightquest";
  src = ./src;
  propagatedBuildInputs = [ pygame numpy ];
}
