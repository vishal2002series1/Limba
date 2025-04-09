import { Component } from '@angular/core';

@Component({
  selector: 'app-retirement-chatbot',
  templateUrl: './retirement-chatbot.component.html',
  styleUrl: './retirement-chatbot.component.scss'
})
export class RetirementChatbotComponent {

  ngOnInit(): void {
    window.location.href = 'https://llm-graph-demo-ui.azurewebsites.net';
  }

}
