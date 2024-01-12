import React from 'react'
import "./NavBarCss.css"
import { Link, useResolvedPath, useMatch } from 'react-router-dom' 

function Sidebar() {
  return (
    <div className='Sidebar'>
      <Link to = "/" className='website_title'> Nightclub Manager</Link>
      <ul>
          <CustomLink to = "/home"> Home </CustomLink>
          <CustomLink to = "/login"> Login </CustomLink>
          {/* <CustomLink to = "/review"> Review </CustomLink>
          <CustomLink to='/rate'> Rate paper </CustomLink> */}
      </ul>
    </div>
  )
}

function CustomLink({ to, children, ...props }) {
  const resolvedPath = useResolvedPath(to)
  const isActive = useMatch({ path: resolvedPath.pathname, end: true })

  return (
    <li className={isActive ? "active" : ""}>
      <Link to={to} {...props}>
        {children}
      </Link>
    </li>
  )
}

export default Sidebar    
