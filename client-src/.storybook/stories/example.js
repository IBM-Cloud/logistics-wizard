import React from 'react';
import { storiesOf, action } from '@kadira/storybook';

storiesOf('Example', module)
  .add('button with text', () => (
    <button onClick={action('Hello!')}>Hello</button>
  ))
  .add('button no text', () => (
    <button />
  ));
