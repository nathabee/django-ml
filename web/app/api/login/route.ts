// web/app/api/login/route.ts
import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const { username, password } = await req.json();
  const backend = process.env.NEXT_PUBLIC_BACKEND_URL || "http://django:8000";

  const r = await fetch(`${backend}/api/auth/login`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  if (!r.ok) {
    return NextResponse.json({ error: "invalid credentials" }, { status: 401 });
  }

  const data = await r.json(); // { access, refresh }
  const res = NextResponse.json({ ok: true });

  // store short-lived access token as HttpOnly cookie
  res.cookies.set("access", data.access, {
    httpOnly: true,
    secure: false,    // set true in prod behind HTTPS
    sameSite: "lax",
    path: "/",
    maxAge: 60 * 15,  // 15 minutes
  });

  // optional: also set refresh if you plan to refresh tokens server-side later
  // res.cookies.set("refresh", data.refresh, {...});

  return res;
}
