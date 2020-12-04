import { Application } from 'stimulus'
import StimulusReflex from 'stimulus_reflex'
import WebsocketConsumer from 'sockpuppet-js'
import Trix_Or_TreatController from './controllers/trix_or_treat_controller'

const application = Application.start()
const consumer = new WebsocketConsumer('ws://localhost:8000/ws/sockpuppet-sync')

application.register("trix_or_treat", Trix_Or_TreatController)
StimulusReflex.initialize(application, { consumer })
