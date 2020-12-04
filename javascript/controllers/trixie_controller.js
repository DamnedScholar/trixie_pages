import { Controller } from 'stimulus';
import StimulusReflex from 'stimulus_reflex';

export default class extends Controller {
  initialize() {
    this.element[this.identifier] = this
  }
  
  connect() {
    StimulusReflex.register(this)
  }
}
