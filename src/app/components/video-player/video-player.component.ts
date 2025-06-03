import { Component } from '@angular/core';

@Component({
  selector: 'app-video-player',
  imports: [],
  templateUrl: './video-player.component.html',
  styleUrl: './video-player.component.css'
})
export class VideoPlayerComponent {
  // video-player.component.ts
videoUrl: string = 'http://localhost:8000/api/video_feed'; // MJPEG stream


}
