import React from 'react'

import classes from './Toolbar.module.css'

// const Logo = React.lazy(() => import('logo'))
const NavigationItems = React.lazy(() =>
  import('../NavigationItems/NavigationItems')
)
const DrawerToggle = React.lazy(() =>
  import('../SideDrawer/DrawerToggle/DrawerToggle')
)

const toolbar = (props) => (
  <header className={classes.Toolbar}>
    <DrawerToggle clicked={props.drawerToggleClicked} />
    <div className={classes.Logo}>
      {/* <Logo /> */}
    </div>
    <nav className={classes.DesktopOnly}>
      <NavigationItems />
    </nav>
  </header>
)

export default toolbar
