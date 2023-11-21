import HomePage from "../pages/home/HomePage";
import WrapperPage from "../pages/home/WrapperPage";
import { RouteType } from "./config";

const appRoutes: RouteType[] = [
    {
        index: true,
        element: <HomePage/>,
        state: 'home',
    },
    {
        index: true,
        element: <WrapperPage/>,
        state: 'predict',
        path: 'predict',
    }
];
export default appRoutes;
