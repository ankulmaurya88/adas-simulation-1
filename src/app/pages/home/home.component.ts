import { Component } from '@angular/core';
import { VideoPlayerComponent } from '../../components/video-player/video-player.component';
import { ControlPanelComponent } from '../../components/control-panel/control-panel.component';
import { AlertPanelComponent } from '../../components/alert-panel/alert-panel.component';
import { FooterComponent } from '../../shared/footer/footer.component';

@Component({
  selector: 'app-home',
  imports: [VideoPlayerComponent,ControlPanelComponent,AlertPanelComponent,FooterComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {

}
