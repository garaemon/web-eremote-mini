/// <reference path="../typings/polymer.d.ts" />

class CommandCell extends Polymer.Element {
  static get is(): string {
    return 'command-cell';
  }

  static get properties(): Object {
    return {
      commandName: {
        type: String,
      },

      commandCode: {
        type: Array,
      },
    };
  }

  public commandName: string;
  public commandCode: number[];

  _onSendTapped(): void {
    this.$.sendQuery.generateRequest()
        .completes
        .then(() => {
          this.$.successToast.text = 'Success to send command';
          this.$.successToast.open();
        })
        .catch(() => {
          alert('Failed to send command');
        });
  }

  _onDeleteTapped(): void {
    this.$.deleteQuery.generateRequest().completes.then((request: any) => {
      if (request.response['found-in-db']) {
        this.$.successToast.text = 'Success to delete command';
      } else {
        this.$.successToast.text = 'Not found in db';
      }
      this.$.successToast.open();
      const event = new Event('command-cell-deleted');
      this.dispatchEvent(event);
    })
  }

  _onShowCodeTapped(): void {
      this.$.codeDialog.open();
  }

  _endpointUri(commandName: string): string {
      return `http://${location.host}/api/sendByName/${commandName}`;
  }
  _onShowEndpointTapped(): void {
      this.$.apiDialog.open();
  }
}

// Need target: es2015
window.customElements.define(CommandCell.is, CommandCell);
