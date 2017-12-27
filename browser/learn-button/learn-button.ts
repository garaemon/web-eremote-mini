/// <reference path="../typings/polymer.d.ts" />

class LearnButton extends Polymer.Element {
  static get is(): string {
    return 'learn-button';
  }
  static get properties(): Object {
    return {
      _ir_code: {
        type: Array,
        value: [],
        notify: true,
      },
    };
  }

  private _ir_code: number[];

  _onTap(): void {
    this.$.spinner.active = true;
    this.$.ajaxLearn.generateRequest()
        .completes
        .then((request: any) => {
          this.$.spinner.active = false;
          const ir_code = request.response.code;
          this._ir_code = ir_code;
          this.$.successDialog.open();
          this.$.successDialog.notifyResize();
        })
        .catch(() => {
          this.$.spinner.active = false;
          this.$.errorDialog.open();
        });
  }

  _onRememberButtonDialogClosed(): void {
    this.$.successDialog.close();
    this.dispatchEvent(new Event('learn-button-command-remembered'));
  }
}

// Need target: es2015
window.customElements.define(LearnButton.is, LearnButton);
