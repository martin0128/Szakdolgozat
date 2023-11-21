import { ReactNode } from "react";

type Props = {
  state?: string;
  children: ReactNode;
};

const PageWrapper = (props: Props) => {
  const { children } = props;
  return <>{children}</>;
};

export default PageWrapper;
