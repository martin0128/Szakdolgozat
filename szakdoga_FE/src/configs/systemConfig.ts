type System = {
  name: string;
  paramLabels: string[];
};

const systems: System[] = [
  {
    name: "Mass Spring Damper",
    paramLabels: ["x", "y", "z"],
  },
  {
    name: "Inverted Pendulum",
    paramLabels: ["y", "z"],
  },
  {
    name: "SIRD",
    paramLabels: ["x", "y", "z", "w"],
  },
  {
    name: "Predator-Prey",
    paramLabels: ["x", "y", "z", "w"],
  },
];

export default systems;
