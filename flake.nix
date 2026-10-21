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
        python = pkgs.python3;

        pythonEnv = python.withPackages (
          ps: with ps; [
            # requirements.txt
            pandas
            astropy
            requests
            ipython
            matplotlib

            # requirements-dev.txt
            requests-mock
            numpydoc
            sphinx
            sphinx-autodoc-typehints
            sphinx-rtd-theme

            # CI tooling (.github/workflows)
            pytest
            coverage
            build

            # Extra development helpers
            pytest-cov
            pytest-xdist
            ipykernel
          ]
        );
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            pythonEnv

            # Formatting / linting
            ruff
            basedpyright

            # Notebook diffs and cleanup (alerce_client.ipynb)
            nbstripout

            # General utilities
            gh
            jq
            yq-go
            httpie
            nixfmt
          ];

          shellHook = ''
            # Use the working tree copy of the package without installing it
            export PYTHONPATH="$PWD''${PYTHONPATH:+:$PYTHONPATH}"
          '';
        };

        formatter = pkgs.nixfmt;
      }
    );
}
