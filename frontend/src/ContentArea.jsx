import React, { useMemo } from "react";
import MarkdownIt from "markdown-it";
import hljs from "highlight.js";
import 'highlight.js/styles/panda-syntax-light.css';
import clsx from "clsx";

const md = new MarkdownIt({
breaks: true,
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return (
          `<pre><code class="hljs">` +
          hljs.highlight(str, { language: lang, ignoreIllegals: true }).value +
          `</code></pre>`
        );
      } catch (__) {}
    }
    return `<pre><code class="hljs">${md.utils.escapeHtml(str)}</code></pre>`;
  },
});

const MarkdownRenderer = ({ content }) => {
  const renderedContent = useMemo(() => md.render(content), [content]);

  return (
    <div
      className={clsx("markdown-container replay_card")}
      dangerouslySetInnerHTML={{ __html: renderedContent }} // Set the HTML content
    />
  );
};

export default MarkdownRenderer;