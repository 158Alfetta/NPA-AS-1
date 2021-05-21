import React from 'react'

import classes from './SideDrawer.module.css'

// const Logo = React.lazy(() => import('Logo'))
const NavigationItems = React.lazy(() =>
  import('../NavigationItems/NavigationItems')
)
const Backdrop = React.lazy(() => import('../../UI/BackDrop/BackDrop'))

const SideDrawer = (props) => {
  let attachedClasses = [classes.SideDrawer, classes.Close]
  if (props.open) {
    attachedClasses = [classes.SideDrawer, classes.open]
  }

  return (
    <>
      <Backdrop show={props.open} clicked={props.closed} />
      <div className={attachedClasses.join(' ')}>
        <div className={classes.Logo}>
          {/* <Logo /> */}
        </div>
        <nav>
          <NavigationItems clicked={props.closed2} />
        </nav>
      </div>
    </>
  )
}

export default SideDrawer
