type System = {
  name: string;
  paramLabels: string[];
  lineNames: string[];
};

const systems: System[] = [
  {
    name: "Mass Spring Damper",
    paramLabels: ["x", "y", "z"],
    lineNames: ["Position", "Velocity"],
  },
  {
    name: "Inverted Pendulum",
    paramLabels: ["y", "z"],
    lineNames: ["Position", "Velocity"],
  },
  {
    name: "SIRD",
    paramLabels: ["x", "y", "z", "w"],
    lineNames: ["Susceptible", "Infected", "Recovered", "Deceased"],
  },
  {
    name: "Predator-Prey",
    paramLabels: ["x", "y", "z", "w"],
    lineNames: ["Prey", "Predator"],
  },
];

export default systems;
