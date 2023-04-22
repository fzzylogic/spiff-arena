// @ts-ignore
import { Content } from '@carbon/react';

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { defineAbility } from '@casl/ability';
import NavigationBar from './components/NavigationBar';

import HomePageRoutes from './routes/HomePageRoutes';
import ErrorBoundary from './components/ErrorBoundary';
import AdminRoutes from './routes/AdminRoutes';
import ProcessRoutes from './routes/ProcessRoutes';

import { AbilityContext } from './contexts/Can';
import UserService from './services/UserService';
import ErrorDisplay from './components/ErrorDisplay';
import APIErrorProvider from './contexts/APIErrorContext';
import Login from './routes/Login';

export default function App() {
  if (!UserService.isLoggedIn()) {
    // This is the wrong thing to do, but need to talk to client.
    // We can not indiscriminately redirect to the SSO as there may be
    // more than one option (facebook, google, etc.) or the user may
    // want to log out of this app, but not out of their SSO account.

    if (document.location.pathname !== '/auth/login') {
      UserService.doLogin();
      return null;
    }
    // If the user logs out of /our app/ then show them a login page
    return Login();
  }

  const ability = defineAbility(() => {});

  return (
    <div className="cds--white">
      {/* @ts-ignore */}
      <AbilityContext.Provider value={ability}>
        <APIErrorProvider>
          <BrowserRouter>
            <NavigationBar />
            <Content>
              <ErrorDisplay />
              <ErrorBoundary>
                <Routes>
                  <Route path="/*" element={<HomePageRoutes />} />
                  <Route path="/tasks/*" element={<HomePageRoutes />} />
                  <Route path="/process/*" element={<ProcessRoutes />} />
                  <Route path="/admin/*" element={<AdminRoutes />} />
                </Routes>
              </ErrorBoundary>
            </Content>
          </BrowserRouter>
        </APIErrorProvider>
      </AbilityContext.Provider>
    </div>
  );
}
