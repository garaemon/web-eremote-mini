/// <reference path="../typings/polymer.d.ts" />

class DetectDevicesButton extends Polymer.Element {
    static get is(): string {
      return 'detect-devices-button';
    }
    static get properties(): Object {
      return {
        _devices: {
          type: Object,
          value: [],
        },
      };
    }

    private _devices : number[];

    _onTap():void {
        this.$.spinner.active = true;
        this.$.queryDevice.generateRequest().completes.then((request: any) => {
          this.$.spinner.active = false;
          this._devices = request.response;
          this.$.successDialog.open();
        }).catch(() => {
          this.$.spinner.active = false;
          alert('faled');
        });
    }

    _computeDeviceNum(_devices: number[]): number {
      return _devices.length;
    }
  }

  // Need target: es2015
  window.customElements.define(DetectDevicesButton.is, DetectDevicesButton);

