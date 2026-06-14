(function () {
  "use strict";

  var copiedTimeout = 1500;
  var copyIcon =
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
    '<rect x="8" y="8" width="11" height="11" rx="2"></rect>' +
    '<path d="M5 15H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v1"></path>' +
    "</svg>";

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }

    return new Promise(function (resolve, reject) {
      var textarea = document.createElement("textarea");
      textarea.value = text;
      textarea.setAttribute("readonly", "");
      textarea.style.position = "fixed";
      textarea.style.top = "-1000px";
      textarea.style.left = "-1000px";
      document.body.appendChild(textarea);
      textarea.focus();
      textarea.select();

      try {
        if (document.execCommand("copy")) {
          resolve();
        } else {
          reject(new Error("Copy command was rejected."));
        }
      } catch (error) {
        reject(error);
      } finally {
        document.body.removeChild(textarea);
      }
    });
  }

  function resetButton(button) {
    button.classList.remove("is-copied", "is-failed");
    button.setAttribute("aria-label", "Copy code");
    button.setAttribute("title", "Copy code");
    button.querySelector(".oceansim-code-copy-text").textContent = "Copied";
  }

  function showStatus(button, className, label) {
    var oldTimer = Number(button.dataset.copyTimer || 0);
    if (oldTimer) {
      window.clearTimeout(oldTimer);
    }

    button.classList.remove("is-copied", "is-failed");
    button.classList.add(className);
    button.setAttribute("aria-label", label);
    button.setAttribute("title", label);
    button.querySelector(".oceansim-code-copy-text").textContent = label;

    button.dataset.copyTimer = String(
      window.setTimeout(function () {
        resetButton(button);
      }, copiedTimeout)
    );
  }

  function addCopyButton(container, pre) {
    if (!container || !pre || container.querySelector(".oceansim-code-copy")) {
      return;
    }

    var text = pre.innerText || pre.textContent || "";
    if (!text.trim()) {
      return;
    }

    container.classList.add("oceansim-code-copy-host");

    var button = document.createElement("button");
    button.type = "button";
    button.className = "oceansim-code-copy";
    button.setAttribute("aria-label", "Copy code");
    button.setAttribute("title", "Copy code");
    button.innerHTML =
      copyIcon + '<span class="oceansim-code-copy-text">Copied</span>';

    button.addEventListener("click", function () {
      var code = pre.innerText || pre.textContent || "";
      copyText(code).then(
        function () {
          showStatus(button, "is-copied", "Copied");
        },
        function () {
          showStatus(button, "is-failed", "Failed");
        }
      );
    });

    container.appendChild(button);
  }

  function prepareLiteralBlock(pre) {
    var wrapper = document.createElement("div");
    wrapper.className =
      "oceansim-code-copy-host oceansim-literal-code-copy-host";
    pre.parentNode.insertBefore(wrapper, pre);
    wrapper.appendChild(pre);
    addCopyButton(wrapper, pre);
  }

  function initCodeCopyButtons() {
    Array.prototype.forEach.call(
      document.querySelectorAll(".rst-content div[class*='highlight-']"),
      function (container) {
        addCopyButton(
          container,
          container.querySelector(".highlight pre") || container.querySelector("pre")
        );
      }
    );

    Array.prototype.forEach.call(
      document.querySelectorAll(".rst-content pre.literal-block"),
      function (pre) {
        if (!pre.closest(".oceansim-code-copy-host")) {
          prepareLiteralBlock(pre);
        }
      }
    );
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initCodeCopyButtons);
  } else {
    initCodeCopyButtons();
  }
})();
