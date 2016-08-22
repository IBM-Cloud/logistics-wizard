import React from 'react';
import { storiesOf } from '@kadira/storybook';

const Headings = () => (
  <div>
    <h1>Heading 1 .h1 <small>small text</small></h1>
    <h2>Heading 2 .h2 <small>small text</small></h2>
    <h3>Heading 3 .h3 <small>small text</small></h3>
    <h4>Heading 4 .h4 <small>small text</small></h4>
    <h5>Heading 5 .h5 <small>small text</small></h5>
    <h6>Heading 6 .h6 <small>small text</small></h6>
    <span className="subheading">Subheading .subheading</span>
  </div>
);

const Paragraphs = () => (
  <div>
    <p>Paragraph text <small>small text</small></p>
    <p>Paragraph Text: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
    <p className="flow-text">This is flow text. Resize the browser to see how it changes. It should look good across views. Use within blog posts or informational bodies that you want to be highly readable. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
  </div>
);

const Modifiers = () => (
  <div>
    <p> <span className="thin">Thin (.thin)</span>, <span className="light">Light (.light)</span>, <small>Small</small>, <em>Emphasis</em> and <strong>Strong</strong> text.</p>
    <h3>h3 text with <span className="thin">Thin (.thin)</span>, <span className="light">Light (.light)</span>, <small>Small</small>, <em>Emphasis</em> and <strong>Strong</strong>.</h3>
  </div>
);

const Lists = () => (
  <div>
    <h4>Ordered List:</h4>
    <ol>
      <li>First item</li>
      <li>Second item</li>
      <li>Third item</li>
    </ol>

    <h4>Unordered List:</h4>
    <ul>
      <li>First item</li>
      <li>Second item</li>
      <li>Third item</li>
    </ul>
  </div>
);

const Other = () => (
  <div>
    <a href="">Link text!</a>

    <blockquote>
      This is an example of text within a blockquote tag.
      <br />
      Another line to make the quote look bigger.
    </blockquote>

    <h4>A horizontal rule:</h4>
    <hr />
  </div>
);

storiesOf('Typography', module)
  .add('Headings', () => (
    <Headings />
  ))
  .add('Paragraphs', () => (
    <Paragraphs />
  ))
  .add('Modifiers', () => (
    <Modifiers />
  ))
  .add('Lists', () => (
    <Lists />
  ))
  .add('Other', () => (
    <Other />
  ));
