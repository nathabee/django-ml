// web/app/api/me/route.ts
import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";

export async function GET(_req: NextRequest) {
  const backend = process.env.NEXT_PUBLIC_BACKEND_URL || "http://django:8000";
  const access = cookies().get("access")?.value;

  if (!access) {
    return NextResponse.json({ error: "not authenticated" }, { status: 401 });
  }

  const r = await fetch(`${backend}/api/me`, {
    headers: { Authorization: `Bearer ${access}` },
    cache: "no-store",
  });

  if (!r.ok) {
    return NextResponse.json({ error: `upstream ${r.status}` }, { status: 502 });
  }

  const data = await r.json();
  return NextResponse.json(data);
}
