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
});
