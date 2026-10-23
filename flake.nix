{
  description = "ALeRCE client development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python312;
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            python
            uv

            # Formatting / linting
            ruff
            basedpyright

            # Notebook rendering
            quarto

            # General utilities
            gh
            jq
            yq-go
            httpie
            nixfmt
          ];

          env.LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
            pkgs.stdenv.cc.cc.lib
            pkgs.zlib
          ];

          shellHook = ''
            if [ ! -d .venv ]; then
              uv venv --python "${python}/bin/python" .venv
            fi

            source .venv/bin/activate

            if [ ! -f .venv/.installed ]; then
              uv pip install -r requirements.txt -r requirements-dev.txt \
                -e . \
                pytest pytest-cov pytest-xdist coverage build \
                ipykernel itables
              touch .venv/.installed
            fi
          '';
        };

        formatter = pkgs.nixfmt;
      }
    );
}
