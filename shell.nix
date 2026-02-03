# shell.nix
let
  pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/d74de548348c46cf25cb1fcc4b74f38103a4590d.tar.gz") {};
in pkgs.mkShell {
  packages = [ 
    pkgs.python314
  ];
  shellHook="
  python -m venv venv
  source venv/bin/activate
  pip3 install Flask Flask-SQLAlchemy
  echo 'done'";
}
