/// <reference path="../typings/polymer.d.ts" />

class RememberButton extends Polymer.Element {
  static get is(): string {
    return 'remember-button';
  }

  static get properties(): Object {
    return {
      code: {
        type: Array,
        value: [],
        notify: true,
      },
      _commandName: String,
    };
  }

  public code: number[];
  private _commandName: string;

  _onTap(): void {
    this.$.inputDialog.open();
  }

  notifyClosed(): void {
    const event = new Event('remember-button-dialog-closed');
    this.dispatchEvent(event);
  }

  _onSaveTapped(): void {
    this.$.spinner.active = true;
    this.$.ajaxRemember.generateRequest()
        .completes
        .then((request: any) => {
          this.$.spinner.active = false;
          if (request.response['existed-in-db']) {
            this.$.successToast.text = `${this._commandName} is overwritten`;
          } else {
            this.$.successToast.text =
                `New command ${this._commandName} is registered`;
          }
          this.$.inputDialog.close();
          this.$.successToast.open();
          this.notifyClosed();
        })
        .catch(() => {
          this.$.spinner.active = false;
          this.$.errorDialog.open();
        });
  }
}

// Need target: es2015
window.customElements.define(RememberButton.is, RememberButton);
