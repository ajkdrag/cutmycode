document.addEventListener("alpine:init", () => {
  Alpine.magic("copy", () => {
    return function () {
      const codeSection = this.$el.closest("section").querySelector("code");
      if (codeSection) {
        const text = codeSection.textContent || codeSection.innerText;
        navigator.clipboard.writeText(text.trim());
        this.copied = true;

        // Revert back to copy icon after 2 seconds
        setTimeout(() => {
          this.copied = false;
        }, 2000);
      }
    };
  });

  Alpine.data("editor", () => {
    // Store CodeMirror instance outside of Alpine's reactive system
    // https://github.com/codemirror/codemirror5/issues/6895
    let editorInstance = null;

    return {
      language: "PYTHON", // Default language

      init() {
        this.setupEditor();
        this.watchLanguageChanges();
      },

      setupEditor() {
        editorInstance = CodeMirror.fromTextArea(this.$refs.editor, {
          mode: this.getEditorMode(this.language),
          lineNumbers: true,
          indentUnit: 4,
          matchBrackets: true,
        });
      },

      watchLanguageChanges() {
        this.$watch("language", (newLanguage) => {
          if (editorInstance) {
            editorInstance.setOption("mode", this.getEditorMode(newLanguage));
          }
        });
      },

      getEditorMode(language) {
        const modes = {
          PYTHON: { name: "python", version: 3, singleLineStringErrors: false },
          JAVASCRIPT: { name: "javascript" },
          // Only allow Python and JavaScript for now
          HTML: { name: "javascript" }, // Fallback to JavaScript
          CSS: { name: "javascript" }, // Fallback to JavaScript
        };
        return modes[language] || modes.PYTHON;
      },
    };
  });
});
