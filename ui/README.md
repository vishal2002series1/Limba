# IRAH UI API Linking

This project includes different tabs for different chats, all utilizing the same reusable component called `common-chat`.

## Financial Planner Data and Graphs
If `financial_planner_user_profile.json` is not showing in Financial Planner then:
```sh
cd ui
npm run prebuild
```

## To Change Endpoint of Existing Tab

To change the endpoint of an existing tab, follow these steps:

1. Navigate to the component's TypeScript file .ts and update the `web_page_type` accordingly.

## To Add a New Tab/Endpoint

To add a new tab with a new endpoint (replace `new-tab` with the desired tab name):

1. Navigate to the components folder to create the new tab component:
```sh
cd ui/src/app/components
ng generate component new-tab-chat
```

2. Add the following code to `new-tab-chat.component.html`:
<app-common-chat [web_page_type]=web_page_type></app-common-chat>

3. In `new-tab-chat.component.ts`, add the endpoint as  web_page_type:
export class NewTabChatComponent {

  web_page_type: string = 'endpoint';
  
}
Replace 'endpoint' with the actual endpoint.

4. In `app-routing.module.ts` add the new tab with its path
const routes: Routes = [

  { path: 'chat/new-tab', component: NewTabChatComponent, title: 'IRAH - NewTab Chat'},

];

5. Update home page `home.component.html` by adding the new page link
    <h1>Welcome to IRAH Chat</h1>
    <ul>

      <li><a routerLink="/chat/new-tab">NewTab Chat</a></li>

    </ul>
