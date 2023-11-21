import React from "react";
import { Link } from "react-router-dom";

type Props = {};

const HomePage = (props: Props) => {
  return (
    <div>
      <Link to={'/predict'}>LOGIN</Link>
    </div>
  );
};

export default HomePage;
