import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Auth/Login.vue';
import Register from '../views/Auth/Register.vue';
import TreeList from '../views/Dashboard/TreeList.vue';
import GraphView from '../views/Tree/GraphView.vue';
import MemberDetail from '../views/Tree/MemberDetail.vue';
import InvitePage from '../views/Tree/InvitePage.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: TreeList,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
  {
    path: '/tree/:id',
    name: 'GraphView',
    component: GraphView,
  },
  {
    path: '/members/:memberId',
    name: 'MemberDetail',
    component: MemberDetail,
  },
  {
    path: '/invite',
    name: 'InvitePage',
    component: InvitePage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;