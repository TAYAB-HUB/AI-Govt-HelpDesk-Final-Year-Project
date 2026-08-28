import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { StatusStamp, PriorityTag, Button } from "./ui";

describe("StatusStamp", () => {
  it("renders the status with underscores turned into spaces", () => {
    render(<StatusStamp status="in_progress" />);
    expect(screen.getByText("in progress")).toBeInTheDocument();
  });

  it("still renders an unrecognized status without crashing", () => {
    render(<StatusStamp status="something_unexpected" />);
    expect(screen.getByText("something unexpected")).toBeInTheDocument();
  });
});

describe("PriorityTag", () => {
  it("renders the priority label as-is", () => {
    render(<PriorityTag priority="urgent" />);
    expect(screen.getByText("urgent")).toBeInTheDocument();
  });
});

describe("Button", () => {
  it("renders its children and responds to clicks", () => {
    let clicked = false;
    render(<Button onClick={() => (clicked = true)}>Save changes</Button>);
    screen.getByText("Save changes").click();
    expect(clicked).toBe(true);
  });

  it("respects the disabled prop", () => {
    render(<Button disabled>Save changes</Button>);
    expect(screen.getByText("Save changes")).toBeDisabled();
  });
});
