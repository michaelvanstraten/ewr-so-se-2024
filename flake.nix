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
      in
      {
        packages =
          (
            let
              inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication;
            in
            {
              default = mkPoetryApplication { projectDir = self; };
            }
          )
          // (
            let
              texlive = pkgs.texliveFull;
              build =
                { description, root-filename }:
                pkgs.stdenvNoCC.mkDerivation {
                  src = ./.;
                  name = description;

                  buildInputs = [ texlive ];

                  TEXMFHOME = "./cache";
                  TEXMFVAR = "./cache/var";

                  buildPhase = ''
                      runHook preBuild

                      SOURCE_DATE_EPOCH="${toString self.lastModified}" latexmk \
                    	-interaction=nonstopmode \
                    	-pdf \
                    	-lualatex \
                    	-pretex="\pdfvariable suppressoptionalinfo 512\relax" \
                    	-usepretex \
                    	"${root-filename}"

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
              approximation-of-pi = {
                report = build {
                  description = "Approximation of Pi (Report)";
                  root-filename = "map.tex";
                };
                presentation = build {
                  description = "Approximation of Pi (Presentation)";
                  root-filename = "presentation.tex";
                };
              };
              harmonic-series = {
                report = build {
                  description = "Harmonic series (Report)";
                  root-filename = "bericht.tex";
                };
                handout = build {
                  description = "Harmonic series (Handout)";
                  root-filename = "bericht_handout.tex";
                };
              };
            }
          );
      }
      // {
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
                package = self.packages.${system}.default.python.pkgs.pylint;
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
          inputsFrom = [ self.packages.${system}.default ];
          inherit (self.checks.${system}.pre-commit-check) shellHook;
          buildInputs = self.checks.${system}.pre-commit-check.enabledPackages;
          packages = with pkgs; [
            poetry
            pyright
          ];
        };
      }
    );
}
