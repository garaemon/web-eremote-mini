/// <reference path="../typings/polymer.d.ts" />

class WebEremoteMiniApp extends Polymer.Element {
  static get is(): string {
    return 'web-eremote-mini-app';
  }
  static get properties(): Object {
    return {prop1: {type: String, value: 'web-eremote-mini-app'}};
  }
}

// Need target: es2015
window.customElements.define(WebEremoteMiniApp.is, WebEremoteMiniApp);
