{
  description = "Application packaged using poetry2nix";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/c49c6a7bf752224177f2098e951c85ca5703d9c3";
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
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication;
      in
      {
        packages.default = mkPoetryApplication { projectDir = self; };
        checks = {
          pre-commit-check = pre-commit-hooks.lib.${system}.run {
            src = ./.;
            hooks = {
              nixfmt = {
                enable = true;
                package = pkgs.nixfmt-rfc-style;
              };
              # Python checks
              mypy = {
                enable = true;
                package = self.packages.${system}.default.python.pkgs.mypy;
              };
              black.enable = true;
              pylint = {
                enable = true;
                package = self.packages.${system}.default.python.pkgs.pylint;
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
