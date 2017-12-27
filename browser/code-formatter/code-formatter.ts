/// <reference path="../typings/polymer.d.ts" />

class CodeFormatter extends Polymer.Element {
  static get is(): string {
    return 'code-formatter';
  }

  static get properties(): Object {
    return {
      code: {
        type: Array,
      },
    };
  }

  public code: number[];
}

// Need target: es2015
window.customElements.define(CodeFormatter.is, CodeFormatter);
