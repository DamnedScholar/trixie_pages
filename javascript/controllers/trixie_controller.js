import { Controller } from 'stimulus';
import StimulusReflex from 'stimulus_reflex';

import Dialog from 'blackstone-ui/presenters/dialog'

export default class extends Controller {
  static targets = ['nav', 'toggle', 'metrics', 'create', 'copy', 'delete']

  initialize() {
    this.element[this.identifier] = this
  }
  
  connect() {
    StimulusReflex.register(this)

    this.hasNavTarget ? this.navTarget.removeAttribute('hidden') : false
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

  edit_mode(e) {
    this.stimulate('TrixieReflex#edit_mode')
  }

  view_mode(e) {
    this.stimulate('TrixieReflex#view_mode')
  }

  async create_page(e) {
    let dialog = await Dialog.prompt().modal({
      'msg': 'Please enter a slug for the new page. This cannot be a slug currently being used.',
      'required': true,
    })

    this.stimulate('TrixieReflex#create_page', dialog.el)
  }

  create_confirm() {
    this.stimulate('TrixieReflex#create_confirm')
  }

  show_metrics(e) {
    this.stimulate('TrixieReflex#show_metrics')
  }

}
