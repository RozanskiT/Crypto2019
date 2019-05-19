struct F
    x::BigInt
    mod::BigInt
    F(x,mod) = new(BigInt(x) % BigInt(mod),BigInt(mod))
end

Base.:!=(a::F, b::F) = (a.x != b.x)
Base.:+(a::F, b::F) = F(a.x + b.x,a.mod)
Base.:-(a::F, b::F) = F(a.x - b.x,a.mod)
Base.:*(a::F, b::F) = F(a.x * b.x,a.mod)
Base.:^(a::F, b::F) = F(a.x ^ b.x,a.mod)
Base.:/(a::F, b::F) = a * b^F(a.mod-2,a.mod)

struct curvPoint
    x::F
    y::F
    d::F
    o::F
end

Base.:+(a::curvPoint, b::curvPoint) = curvPoint(
                        (a.x*b.y + b.x*a.y)/(a.o + a.d*a.x*a.y*b.x*b.y),
                        (a.x*b.y - b.x*a.y)/(a.o - a.d*a.x*a.y*b.x*b.y),
                        a.d,
                        a.o)
function Base.show(io::IO, p::curvPoint)
    print(io,"(",p.x.x,", ",p.y.x,",(mod)",p.x.mod,")")
end

N = 1009
d = F(-11,N)
o = F(1,N)

P1 = curvPoint(F(7,N),F(415,N),d,o)
P2 = curvPoint(F(23,N),F(487,N),d,o)
print(P1+P2)
