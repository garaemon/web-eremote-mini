// TODO: remove this file after polymer 2.4 is released
declare namespace Polymer {
  class Element {
    public $: any;
    public dispatchEvent(evt: Event): boolean;
    public addEventListener(eventName: string, callback: (evt: Event) => void):
        void;
    public connectedCallback(): void;
  }
}
