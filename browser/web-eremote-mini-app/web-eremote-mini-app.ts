/// <reference path="../typings/polymer.d.ts" />

class WebEremoteMiniApp extends Polymer.Element {
  static get is(): string {
    return 'web-eremote-mini-app';
  }

  static get properties(): Object {
    return {};
  }

  _onLearnButtonCommandRemembered(): void {
    this.$.commandList.updateCommandList();
  }
}

// Need target: es2015
window.customElements.define(WebEremoteMiniApp.is, WebEremoteMiniApp);
