
/*
    pbrt source code is Copyright(c) 1998-2016
                        Matt Pharr, Greg Humphreys, and Wenzel Jakob.

    This file is part of pbrt.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are
    met:

    - Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    - Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
    IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
    TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
    HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

 */

#if defined(_MSC_VER)
#define NOMINMAX
#pragma once
#endif

#ifndef PBRT_SHAPES_TRIANGLE_H
#define PBRT_SHAPES_TRIANGLE_H

// shapes/triangle.h*
#include "shape.h"
#include "stats.h"
#include <map>

namespace pbrt {

STAT_MEMORY_COUNTER("Memory/Triangle meshes", triMeshBytes);

struct DynamicTriangleMesh
{
    std::vector< int > vertexIndices;
    std::vector< Point3f > p;
    std::vector< Normal3f > n;
    std::vector< Vector3f > s;
    std::vector< Point2f > uv;
    std::shared_ptr <Texture< Float > > alphaMask, shadowAlphaMask;
    int nTriangles = 0;

    int AddInterpolatedVertex( int firstIndex, int secondIndex, float amt = 0.5f )
    {
        p.push_back( amt * (p[firstIndex] + p[secondIndex]) );
        if ( n.size() )
        {
            Normal3f norm = Normalize( amt * (n[firstIndex] + n[secondIndex]) );
            n.push_back( norm );
        }
        if ( s.size() )
            s.push_back( amt * (s[firstIndex] + s[secondIndex]) );
        if ( uv.size() )
            uv.push_back( amt * (uv[firstIndex] + uv[secondIndex]) );
        return static_cast< int >( p.size() - 1 );
    }
};

// Triangle Declarations
struct TriangleMesh {
    // TriangleMesh Public Methods
    TriangleMesh() = default;
    TriangleMesh(const Transform &ObjectToWorld, int nTriangles,
                 const int *vertexIndices, int nVertices, const Point3f *P,
                 const Vector3f *S, const Normal3f *N, const Point2f *uv,
                 const std::shared_ptr<Texture<Float>> &alphaMask,
                 const std::shared_ptr<Texture<Float>> &shadowAlphaMask,
                 const int *faceIndices);

    // TriangleMesh Data
    int nTriangles, nVertices;
    std::vector<int> vertexIndices;
    std::unique_ptr<Point3f[]> p;
    std::unique_ptr<Normal3f[]> n;
    std::unique_ptr<Vector3f[]> s;
    std::unique_ptr<Point2f[]> uv;
    std::shared_ptr<Texture<Float>> alphaMask, shadowAlphaMask;
    std::vector<int> faceIndices;
};

class Triangle : public Shape {
  public:
    // Triangle Public Methods
    Triangle(const Transform *ObjectToWorld, const Transform *WorldToObject,
             bool reverseOrientation, const std::shared_ptr<TriangleMesh> &mesh,
             int triNumber)
        : Shape(ObjectToWorld, WorldToObject, reverseOrientation), mesh(mesh) {
        v = &mesh->vertexIndices[3 * triNumber];
        triMeshBytes += sizeof(*this);
        faceIndex = mesh->faceIndices.size() ? mesh->faceIndices[triNumber] : 0;
    }

    Triangle( const Transform *ObjectToWorld, const Transform *WorldToObject,
             bool reverseOrientation, const int* indices )
        : Shape(ObjectToWorld, WorldToObject, reverseOrientation)
    {
        v = indices;
    }

    Bounds3f ObjectBound() const;
    Bounds3f WorldBound() const;
    bool Intersect(const Ray &ray, Float *tHit, SurfaceInteraction *isect,
                   bool testAlphaTexture = true) const;
    bool IntersectP(const Ray &ray, bool testAlphaTexture = true) const;
    Float Area() const;

    int NumSubdividedTris( float threshold ) const;
    int Subdivide( float threshold, std::vector< std::shared_ptr< Shape > >& newShapes,
                         DynamicTriangleMesh& dynamicMesh, const std::shared_ptr< TriangleMesh >& newMesh );

    virtual bool IsSplitClippingSupported() const
    {
        return true;
    }

    virtual std::shared_ptr<Shape> NewShape() const
    {
        return std::make_shared<Triangle>( *this );
    }

    using Shape::Sample;  // Bring in the other Sample() overload.
    Interaction Sample(const Point2f &u, Float *pdf) const;

    // Returns the solid angle subtended by the triangle w.r.t. the given
    // reference point p.
    Float SolidAngle(const Point3f &p, int nSamples = 0) const;

    std::shared_ptr<TriangleMesh> mesh;

  private:
    // Triangle Private Methods
    void GetUVs(Point2f uv[3]) const {
        if (mesh->uv) {
            uv[0] = mesh->uv[v[0]];
            uv[1] = mesh->uv[v[1]];
            uv[2] = mesh->uv[v[2]];
        } else {
            uv[0] = Point2f(0, 0);
            uv[1] = Point2f(1, 0);
            uv[2] = Point2f(1, 1);
        }
    }

    // Triangle Private Data
    
    const int *v;
    int faceIndex;
};

std::vector<std::shared_ptr<Shape>> CreateTriangleMesh(
    const Transform *o2w, const Transform *w2o, bool reverseOrientation,
    int nTriangles, const int *vertexIndices, int nVertices, const Point3f *p,
    const Vector3f *s, const Normal3f *n, const Point2f *uv,
    const std::shared_ptr<Texture<Float>> &alphaTexture,
    const std::shared_ptr<Texture<Float>> &shadowAlphaTexture,
    const int *faceIndices = nullptr);
std::vector<std::shared_ptr<Shape>> CreateTriangleMeshShape(
    const Transform *o2w, const Transform *w2o, bool reverseOrientation,
    const ParamSet &params,
    std::map<std::string, std::shared_ptr<Texture<Float>>> *floatTextures =
        nullptr);

bool WritePlyFile(const std::string &filename, int nTriangles,
                  const int *vertexIndices, int nVertices, const Point3f *P,
                  const Vector3f *S, const Normal3f *N, const Point2f *UV,
                  const int *faceIndices);

}  // namespace pbrt

#endif  // PBRT_SHAPES_TRIANGLE_H
