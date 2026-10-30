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

            # GitHub Actions auditing
            zizmor
            actionlint

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

            # Reinstall whenever the requirements change.
            req_hash=$(cat requirements.txt requirements-dev.txt | sha256sum | cut -d' ' -f1)
            if [ "$(cat .venv/.installed 2>/dev/null)" != "$req_hash" ]; then
              uv pip install -r requirements.txt -r requirements-dev.txt \
                -e . \
                pytest-cov pytest-xdist build \
                ipykernel itables
              echo "$req_hash" > .venv/.installed
            fi
          '';
        };

        formatter = pkgs.nixfmt;
      }
    );
}
