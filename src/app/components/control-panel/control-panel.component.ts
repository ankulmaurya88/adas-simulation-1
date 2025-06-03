import { Component } from '@angular/core';
// import { SimulationService } from '../../core/services/simulation.service';
import { SimulationService } from '../../core/services/simulation.service';


@Component({
  selector: 'app-control-panel',
  // imports: [SimulationService,],
  templateUrl: './control-panel.component.html',
  styleUrl: './control-panel.component.css'
})
export class ControlPanelComponent {
  // startSimulation() {
  //   this.simulationService.start().subscribe();
  // }
  // pauseSimulation() {
  //   this.simulationService.pause().subscribe();
  // }


  constructor(private simulationService: SimulationService) {}

  // startSimulation() {
  //   this.simulationService.start().subscribe();
  // }

  // pauseSimulation() {
  //   this.simulationService.pause().subscribe();
  // }

}
