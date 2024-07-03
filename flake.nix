{
  description = "Application packaged using poetry2nix";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    pre-commit-hooks.url = "github:cachix/pre-commit-hooks.nix";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      poetry2nix,
      pre-commit-hooks,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication mkPoetryEnv;
        ewr-so-se-2024 = mkPoetryApplication { projectDir = ./.; };
      in
      {
        apps = {
          approximation-of-pi = {
            type = "app";
            program = "${ewr-so-se-2024}/bin/approximation-of-pi";
          };
          harmonic-series = {
            type = "app";
            program = "${ewr-so-se-2024}/bin/harmonic-series";
          };
        };
      }
      // {
        packages =
          let
            build =
              {
                src ? ./.,
                name,
                root-filename,
              }:
              pkgs.stdenvNoCC.mkDerivation {
                inherit src name;

                buildInputs = with pkgs; [
                  coreutils
                  ncurses
                  texliveFull
                  inkscape
                ];

                TEXMFHOME = "./cache";
                TEXMFVAR = "./cache/var";

                XDG_CACHE_HOME = "$(mktemp -d)";

                buildPhase = ''
                  export PATH="/usr/sbin:$PATH"
                  runHook preBuild

                  SOURCE_DATE_EPOCH="${toString self.lastModified}" latexmk \
                    -interaction=nonstopmode \
                    -pdf \
                    -lualatex \
                    -shell-escape \
                    -pretex="\pdfvariable suppressoptionalinfo 512\relax" \
                    -usepretex \
                    "${toString root-filename}"

                  runHook postBuild
                '';

                installPhase = ''
                  runHook preInstall

                  install -d $out && install -m644 -D *.pdf $out/

                  runHook postInstall
                '';
              };
          in
          {
            default = ewr-so-se-2024;

            approximation-of-pi-report = build {
              src = ./src/approximation-of-pi;
              name = "Approximation of Pi (Report)";
              root-filename = "bericht.tex";
            };
            approximation-of-pi-presentation = build {
              src = ./src/approximation-of-pi;
              name = "Approximation of Pi (Presentation)";
              root-filename = "presentation.tex";
            };

            harmonic-series-report = build {
              src = ./src/harmonic-series;
              name = "Harmonic series (Report)";
              root-filename = "bericht.tex";
            };
            harmonic-series-handout = build {
              src = ./src/harmonic-series;
              name = "Harmonic series (Handout)";
              root-filename = "bericht_handout.tex";
            };
          };
      }
      // (
        let
          poetry-enviorment = mkPoetryEnv { projectDir = ./.; };
        in
        rec {
          checks = {
            pre-commit-check = pre-commit-hooks.lib.${system}.run {
              src = ./.;
              hooks = {
                nixfmt = {
                  enable = true;
                  package = pkgs.nixfmt-rfc-style;
                };
                # Python checks
                black.enable = true;
                pylint = {
                  enable = true;
                  settings = {
                    binPath = "${poetry-enviorment}/bin/python -m pylint";
                  };
                };
                # Formatting check for LaTeX
                latexindent = {
                  enable = true;
                  settings = {
                    flags = "--local --silent --modifylinebreak --overwriteIfDifferent";
                  };
                };
              };
            };
          };

          devShells.default = pkgs.mkShell {
            inputsFrom = [ ewr-so-se-2024 ];
            inherit (checks.pre-commit-check) shellHook;
            packages = with pkgs; [
              poetry
              pyright
              texlab
              black
              texliveFull
            ];
          };
        }
      )
    );
}
