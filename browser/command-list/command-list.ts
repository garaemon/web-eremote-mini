/// <reference path="../typings/polymer.d.ts" />

class CommandList extends Polymer.Element {
  static get is(): string {
    return 'command-list';
  }

  static get properties(): Object {
    return {
      _commands: {type: Array, notify: true},
    };
  }

  private _commands: Object;

  updateCommandList(): void {
    this.$.queryCommands.generateRequest()
        .completes
        .then((request: any) => {
          this._commands = request.response;
        })
        .catch(
            () => {

            });
  }

  connectedCallback(): void {
    super.connectedCallback();
    this.updateCommandList();
  }

  _onCommandCellDeleted(): void {
    this.updateCommandList();
  }

}

// Need target: es2015
window.customElements.define(CommandList.is, CommandList);
