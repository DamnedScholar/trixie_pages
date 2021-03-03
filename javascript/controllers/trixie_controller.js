import { Controller } from 'stimulus';
import StimulusReflex from 'stimulus_reflex';

import Prompt from 'blackstone-ui/presenters/dialog/prompt'
import { html } from 'lit-html'

export default class extends Controller {
  static targets = ['nav', 'toggle', 'metrics', 'create', 'copy', 'delete']

  initialize() {
    this.element[this.identifier] = this
  }
  
  connect() {
    StimulusReflex.register(this)

    this.hasNavTarget ? this.navTarget.removeAttribute('hidden') : false
  }

  disconnect() {
  }

  // Lifecycle methods

  // beforeReflex(anchor, reflex) {
  //   console.log(anchor)
  //   console.log(reflex)
  // }

  afterReflex(anchor, reflex, error) {
    console.log(anchor)
    console.log(reflex)
    console.log(error)
  }

  // Reflex API

  editMode(e) {
    this.stimulate('TrixieReflex#edit_mode')
  }

  viewMode(e) {
    this.stimulate('TrixieReflex#view_mode')
  }

  beforeCreatePageReflex(anchor, reflex) {
    // Generate a dialog to receive input. The property will be a Promise until it resolves, and resolution will be based on data back from the server.
    document.addEventListener("slug-prompt", e => {
      this.dialog = new Prompt({
        getHTML: () => html`${e.detail}`,
        btns: ['submit', 'cancel']
      })
    })
  }

  createPage() {
    this.stimulate('TrixieReflex#create_page')
  }

  createConfirm() {
    this.stimulate('TrixieReflex#create_confirm')
  }

  showMetrics(e) {
    this.stimulate('TrixieReflex#show_metrics')
  }

}
